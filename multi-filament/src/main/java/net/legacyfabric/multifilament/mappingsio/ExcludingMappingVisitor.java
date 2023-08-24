package net.legacyfabric.multifilament.mappingsio;

import java.io.IOException;
import java.util.List;
import java.util.Set;

import net.fabricmc.mappingio.MappedElementKind;
import net.fabricmc.mappingio.MappingFlag;
import net.fabricmc.mappingio.MappingVisitor;
import net.fabricmc.mappingio.tree.MappingTree;
import net.fabricmc.mappingio.tree.MemoryMappingTree;

public class ExcludingMappingVisitor implements MappingVisitor {
	private final MappingVisitor parent;
	private final MemoryMappingTree mappingTree;
	private final int namespaceId;
	private MappingTree.ClassMapping currentClass;
	private MappingTree.FieldMapping currentField;
	private MappingTree.MethodMapping currentMethod;

	public ExcludingMappingVisitor(MappingVisitor parent, MemoryMappingTree mappingTree) {
		this.parent = parent;
		this.mappingTree = mappingTree;
		this.namespaceId = this.mappingTree.getNamespaceId("intermediary");
	}

	@Override
	public Set<MappingFlag> getFlags() {
		return parent.getFlags();
	}

	@Override
	public void reset() {
		parent.reset();
	}

	@Override
	public boolean visitHeader() throws IOException {
		return parent.visitHeader();
	}

	@Override
	public void visitNamespaces(String srcNamespace, List<String> dstNamespaces) throws IOException {
		parent.visitNamespaces(srcNamespace, dstNamespaces);
	}

	@Override
	public void visitMetadata(String key, String value) throws IOException {
		parent.visitMetadata(key, value);
	}

	@Override
	public boolean visitContent() throws IOException {
		return parent.visitContent();
	}

	@Override
	public boolean visitClass(String srcName) throws IOException {
		this.currentClass = this.mappingTree.getClass(srcName, this.namespaceId);

		return parent.visitClass(srcName);
	}

	@Override
	public boolean visitField(String srcName, String srcDesc) throws IOException {
		if (this.currentClass != null) {
			this.currentField = this.currentClass.getField(srcName, srcDesc, this.namespaceId);

			if (this.currentField != null) {
				return false;
			}
		}

		return parent.visitField(srcName, srcDesc);
	}

	@Override
	public boolean visitMethod(String srcName, String srcDesc) throws IOException {
		if (this.currentClass != null) {
			this.currentMethod = this.currentClass.getMethod(srcName, srcDesc, this.namespaceId);

			if (this.currentMethod != null) {
				return false;
			}
		}

		return parent.visitMethod(srcName, srcDesc);
	}

	@Override
	public boolean visitMethodArg(int argPosition, int lvIndex, String srcName) throws IOException {
		return parent.visitMethodArg(argPosition, lvIndex, srcName);
	}

	@Override
	public boolean visitMethodVar(int lvtRowIndex, int lvIndex, int startOpIdx, String srcName) throws IOException {
		return parent.visitMethodVar(lvtRowIndex, lvIndex, startOpIdx, srcName);
	}

	@Override
	public boolean visitEnd() throws IOException {
		return parent.visitEnd();
	}

	@Override
	public void visitDstName(MappedElementKind targetKind, int namespace, String name) throws IOException {
		parent.visitDstName(targetKind, namespace, name);
	}

	@Override
	public void visitDstDesc(MappedElementKind targetKind, int namespace, String desc) throws IOException {
		parent.visitDstDesc(targetKind, namespace, desc);
	}

	@Override
	public boolean visitElementContent(MappedElementKind targetKind) throws IOException {
		return parent.visitElementContent(targetKind);
	}

	@Override
	public void visitComment(MappedElementKind targetKind, String comment) throws IOException {
		parent.visitComment(targetKind, comment);
	}
}
